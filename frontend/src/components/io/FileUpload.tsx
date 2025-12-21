// import { useState } from "react";
// import { Input } from "../ui/input";
// import { Button } from "../ui/button";

// const FileUpload = () => {
//   const [file, setFile] = useState<File | null>(null);
//   async function handleFileUpload() {
//     if (!file) return;
//     const formData = new FormData();
//     formData.append("file", file);
//     try {
//       await axios.post("...", formData, {
//         headers: { "Content-Type": "multipart/form-data" },
//       });
//     } catch {
//       return;
//     }
//   }

//   const formData = new FormData();
//   formData.append("file", csvFile);

//   await fetch("/api/upload", {
//     method: "POST",
//     body: formData,
//   }); // better

//   const fd = new FormData();
//   fd.append("file", file);
//   fd.append("name", datasetName);
//   fd.append("uploader_id", userId);
//   fd.append("source", "ui");

//   const inputRef = useRef<HTMLInputElement | null>(null);

//   function handleRemove() {
//     setFile(null);
//     if (inputRef.current) inputRef.current.value = ""; // important
//   }

//   return (
//     <div>
//       <Input
//         type="file"
//         accept=".csv,text/csv"
//         multiple={false}
//         onChange={(e) => {
//           if (e.target.files) setFile(e.target.files[0]);
//         }}
//       />
//       <Button>Upload</Button>
//     </div>
//   );
// };

// export default FileUpload;
