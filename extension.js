const vscode = require("vscode");
const fs = require("fs/promises");
const os = require("os");
const path = require("path");

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
    const template = "Input: \nOutput: \n";
    await fs.writeFile(caseFilePath, template, "utf8");
  }

  const doc = await vscode.workspace.openTextDocument(caseFilePath);
  await vscode.window.showTextDocument(doc, { preview: false });
}

async function debugCurrentSolution(context) {
  const editor = getActivePythonEditor();
  if (!editor) {
    void vscode.window.showErrorMessage("Open a Python solution file first.");
    return;
  }

  if (!hasPythonDebugger()) {
    void vscode.window.showErrorMessage(
      "Python Debugger extension is required to start this debug session."
    );
    return;
  }

  await ensureSaved(editor.document);

  const solutionPath = editor.document.uri.fsPath;
  const caseFilePath = getCaseFilePath(solutionPath);

  try {
    await fs.access(caseFilePath);
  } catch {
    const choice = await vscode.window.showInformationMessage(
      "Same-name .txt case file not found. Create it now?",
      "Create",
      "Cancel"
    );
    if (choice !== "Create") {
      return;
    }
    await fs.writeFile(caseFilePath, "Input: \nOutput: \n", "utf8");
    const doc = await vscode.workspace.openTextDocument(caseFilePath);
    await vscode.window.showTextDocument(doc, { preview: false });
    return;
  }

  await ensureCaseDocumentSaved(caseFilePath);

  const { bootstrapPath, runtimeDir } = await ensureHelperRuntime(context);
  const folder = vscode.workspace.getWorkspaceFolder(editor.document.uri);

  const configuration = {
    name: "LeetCode: Debug Current Solution",
    type: "debugpy",
    request: "launch",
    program: bootstrapPath,
    args: ["--solution", solutionPath, "--case-file", caseFilePath],
    cwd: path.dirname(solutionPath),
    console: "integratedTerminal",
    justMyCode: true,
    stopOnEntry: false,
    subProcess: false,
    rules: [
      {
        path: runtimeDir,
        include: false,
      },
    ],
    env: {
      IDE_PROJECT_ROOTS: path.dirname(solutionPath),
      PYDEVD_FILTERS: JSON.stringify({
        [bootstrapPath]: true,
        [path.join(runtimeDir, "*.py")]: true,
        [path.join(runtimeDir, "**")]: true,
      }),
    },
  };

  const started = await vscode.debug.startDebugging(folder, configuration);
  if (!started) {
    void vscode.window.showErrorMessage("Failed to start the LeetCode debug session.");
  }
}

function activate(context) {
  context.subscriptions.push(
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
