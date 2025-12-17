import { useParams } from "react-router-dom";
import PredictFormDrawer from "@/components/ml/predict/PredictFormDrawer";

const ModelIdPage = () => {
  const params = useParams<{
    datasetId: string;
    datasetVersionId: string;
    problemId: string;
    modelId: string;
  }>();
  if (!params.modelId) {
    throw new Error("modelId param missing");
  }
  const problemId = params.problemId;
  const modelId = params.modelId;

  return (
    <div className="min-w-full flex flex-col items-center justify-center">
      <h1>Model: {modelId}</h1>
      <PredictFormDrawer problemId={problemId} modelId={modelId} />
    </div>
  );
};

export default ModelIdPage;
