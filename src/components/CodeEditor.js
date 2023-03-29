import Editor from "@monaco-editor/react"

const options = {
  minimap: {
    enabled: false
  }
}

export default function CodeEditor() {
  return (
    <>
      <Editor
        height="400px"
        defaultLanguage="javascript"
        defaultValue="// some comment"
        theme="vs-dark"
        options={options}
      />
    </>
  )
}