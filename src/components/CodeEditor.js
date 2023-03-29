import Editor from "@monaco-editor/react";

export default function CodeEditor() {

    function handleEditorChange(value, event) {
        console.log("onChange: the editor instance:", value);
        console.log("onChange: the monaco instance:", event);
    }

    function handleEditorDidMount(editor, monaco) {
        console.log("onMount: the editor instance:", editor);
        console.log("onMount: the monaco instance:", monaco);
    }

    function handleEditorWillMount(monaco) {
        console.log("beforeMount: the monaco instance:", monaco);
    }

    function handleEditorValidation(markers) {
        // model markers
        // markers.forEach(marker => console.log('onValidate:', marker.message));
    }

    return (
        <Editor
            height="90vh"
            onChange={handleEditorChange}
            onMount={handleEditorDidMount}
            beforeMount={handleEditorWillMount}
            onValidate={handleEditorValidation}
            defaultLanguage="javascript"
            defaultValue="// some comment"
        />
    );
}