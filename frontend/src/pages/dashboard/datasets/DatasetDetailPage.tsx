import { useParams } from "react-router-dom";

const DatasetDetailPage = () => {
  const { datasetId } = useParams<{ datasetId: string }>();
  return <div>Dataset: {datasetId}</div>;
};

export default DatasetDetailPage;
