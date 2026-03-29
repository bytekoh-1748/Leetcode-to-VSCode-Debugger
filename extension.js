const vscode = require("vscode");
const fs = require("fs/promises");
const os = require("os");
const path = require("path");

const LEETCODE_DEBUG_TYPE = "leetcodeDebugger";
const LEETCODE_DEBUG_NAME = "LeetCode: Debug Current Solution";
const CASE_FILE_TEMPLATE = "Input: \nOutput: \n";

function getActivePythonEditor() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    return undefined;
  }

  const { document } = editor;
  if (document.uri.scheme !== "file" || document.languageId !== "python") {
    return undefined;
  }

  return editor;
}

function getCaseFilePath(solutionPath) {
  const parsed = path.parse(solutionPath);
  return path.join(parsed.dir, `${parsed.name}.txt`);
}

async function ensureSaved(document) {
  if (document.isDirty) {
    await document.save();
  }
}

async function ensureCaseDocumentSaved(caseFilePath) {
  for (const document of vscode.workspace.textDocuments) {
    if (document.uri.scheme === "file" && document.uri.fsPath === caseFilePath) {
      await ensureSaved(document);
      return;
    }
  }
}

function hasPythonDebugger() {
  return Boolean(
    vscode.extensions.getExtension("ms-python.debugpy") ||
      vscode.extensions.getExtension("ms-python.python")
  );
}

async function ensureHelperRuntime(context) {
  const sourceDir = path.join(context.extensionPath, "python");
  const runtimeDir = path.join(os.tmpdir(), "leetcode-debugger-runtime");
  const files = ["bootstrap_debug_session.py", "leetcode_debug_runtime.py"];

  await fs.mkdir(runtimeDir, { recursive: true });
  await Promise.all(
    files.map((name) =>
      fs.copyFile(path.join(sourceDir, name), path.join(runtimeDir, name))
    )
  );
  return {
    bootstrapPath: path.join(runtimeDir, "bootstrap_debug_session.py"),
    runtimeDir,
  };
}

async function openCaseFile() {
  const editor = getActivePythonEditor();
  if (!editor) {
    void vscode.window.showErrorMessage("Open a Python solution file first.");
    return;
  }

  await ensureSaved(editor.document);

  const caseFilePath = getCaseFilePath(editor.document.uri.fsPath);
  try {
    await fs.access(caseFilePath);
  } catch {
    await fs.writeFile(caseFilePath, CASE_FILE_TEMPLATE, "utf8");
  }

  const doc = await vscode.workspace.openTextDocument(caseFilePath);
  await vscode.window.showTextDocument(doc, { preview: false });
}

async function resolveSolutionPath(explicitSolutionPath) {
  if (explicitSolutionPath) {
    try {
      const document = await vscode.workspace.openTextDocument(explicitSolutionPath);
      if (document.languageId !== "python") {
        void vscode.window.showErrorMessage("The configured solution file must be a Python file.");
        return undefined;
      }
      await ensureSaved(document);
      return document.uri.fsPath;
    } catch {
      void vscode.window.showErrorMessage("The configured solution file could not be opened.");
      return undefined;
    }
  }

  const editor = getActivePythonEditor();
  if (!editor) {
    void vscode.window.showErrorMessage("Open a Python solution file first.");
    return undefined;
  }

  await ensureSaved(editor.document);
  return editor.document.uri.fsPath;
}

async function ensureCaseFileReady(caseFilePath) {
  try {
    await fs.access(caseFilePath);
    return true;
  } catch {
    const choice = await vscode.window.showInformationMessage(
      "Same-name .txt case file not found. Create it now?",
      "Create",
      "Cancel"
    );
    if (choice !== "Create") {
      return false;
    }

    await fs.writeFile(caseFilePath, CASE_FILE_TEMPLATE, "utf8");
    const doc = await vscode.workspace.openTextDocument(caseFilePath);
    await vscode.window.showTextDocument(doc, { preview: false });
    return false;
  }
}

async function resolveLeetCodeDebugConfiguration(context, debugConfiguration = {}) {
  if (!hasPythonDebugger()) {
    void vscode.window.showErrorMessage(
      "Python Debugger extension is required to start this debug session."
    );
    return undefined;
  }

  const solutionPath = await resolveSolutionPath(debugConfiguration.solution);
  if (!solutionPath) {
    return undefined;
  }

  const caseFilePath = debugConfiguration.caseFile || getCaseFilePath(solutionPath);
  const isCaseFileReady = await ensureCaseFileReady(caseFilePath);
  if (!isCaseFileReady) {
    return undefined;
  }

  await ensureCaseDocumentSaved(caseFilePath);
  const { bootstrapPath, runtimeDir } = await ensureHelperRuntime(context);
  const env = {
    ...(debugConfiguration.env || {}),
  };
  env.IDE_PROJECT_ROOTS ??= path.dirname(solutionPath);
  env.PYDEVD_FILTERS ??= JSON.stringify({
    [bootstrapPath]: true,
    [path.join(runtimeDir, "*.py")]: true,
    [path.join(runtimeDir, "**")]: true,
  });

  const resolvedConfiguration = {
    ...debugConfiguration,
    name: debugConfiguration.name || LEETCODE_DEBUG_NAME,
    type: "debugpy",
    request: "launch",
    program: bootstrapPath,
    args: ["--solution", solutionPath, "--case-file", caseFilePath],
    cwd: debugConfiguration.cwd || path.dirname(solutionPath),
    console: debugConfiguration.console || "integratedTerminal",
    justMyCode: debugConfiguration.justMyCode ?? true,
    stopOnEntry: debugConfiguration.stopOnEntry ?? false,
    subProcess: debugConfiguration.subProcess ?? false,
    rules: [
      {
        path: runtimeDir,
        include: false,
      },
    ],
    env,
  };

  delete resolvedConfiguration.solution;
  delete resolvedConfiguration.caseFile;
  return resolvedConfiguration;
}

class LeetCodeDebugConfigurationProvider {
  constructor(context) {
    this.context = context;
  }

  resolveDebugConfiguration(folder, debugConfiguration) {
    return debugConfiguration;
  }

  async resolveDebugConfigurationWithSubstitutedVariables(folder, debugConfiguration) {
    return resolveLeetCodeDebugConfiguration(this.context, debugConfiguration);
  }
}

class LeetCodeDynamicConfigurationProvider {
  provideDebugConfigurations() {
    return [
      {
        name: LEETCODE_DEBUG_NAME,
        type: LEETCODE_DEBUG_TYPE,
        request: "launch",
      },
    ];
  }
}

async function debugCurrentSolution(context) {
  const editor = getActivePythonEditor();
  if (!editor) {
    void vscode.window.showErrorMessage("Open a Python solution file first.");
    return;
  }

  const folder = vscode.workspace.getWorkspaceFolder(editor.document.uri);
  const configuration = await resolveLeetCodeDebugConfiguration(context, {
    name: LEETCODE_DEBUG_NAME,
    type: LEETCODE_DEBUG_TYPE,
    request: "launch",
    solution: editor.document.uri.fsPath,
    caseFile: getCaseFilePath(editor.document.uri.fsPath),
  });
  if (!configuration) {
    return;
  }

  const started = await vscode.debug.startDebugging(folder, configuration);
  if (!started) {
    void vscode.window.showErrorMessage("Failed to start the LeetCode debug session.");
  }
}

function activate(context) {
  const debugConfigurationProvider = new LeetCodeDebugConfigurationProvider(context);
  const dynamicConfigurationProvider = new LeetCodeDynamicConfigurationProvider();

  context.subscriptions.push(
    vscode.debug.registerDebugConfigurationProvider(
      LEETCODE_DEBUG_TYPE,
      debugConfigurationProvider
    ),
    vscode.debug.registerDebugConfigurationProvider(
      LEETCODE_DEBUG_TYPE,
      dynamicConfigurationProvider,
      vscode.DebugConfigurationProviderTriggerKind.Dynamic
    ),
    vscode.commands.registerCommand("leetcodeDebugger.openCaseFile", openCaseFile),
    vscode.commands.registerCommand("leetcodeDebugger.debugCurrentSolution", () =>
      debugCurrentSolution(context)
    )
  );
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
};
