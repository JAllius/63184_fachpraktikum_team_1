import { useCallback, useEffect, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import { PageSize, Pagination } from "@/components/table";
import Loading from "@/components/loading/Loading";
import { get_prediction, type Prediction } from "@/lib/actions/predictions";
import PredictionTable from "@/components/prediction_details/PredicitonTable";
import NotFound from "@/components/errors/not_found/NotFound";

const PredictionDetailPage = () => {
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
  const [prediction, setPrediction] = useState<Prediction | null>(null);

  const page = Number(searchParams.get("page") ?? 1);
  const size = Number(searchParams.get("size") ?? 20);
  //   const totalRows = rows.length;
  //   const totalPages = Math.max(1, Math.ceil(totalRows / size));
  //   total_pages = int((total + size -1)/size) if size > 0 else 1

  const params = useParams<{ predictionId: string }>();
  if (!params.predictionId) {
    throw new Error("predictionId param missing");
  }
  const predictionId = params.predictionId;

  const loadPrediction = useCallback(async () => {
    try {
      const data: Prediction = await get_prediction(predictionId);
      setPrediction(data);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }, [predictionId]);

  useEffect(() => {
    loadPrediction();
  }, [loadPrediction]);

  const outputs_json = prediction?.outputs_json
    ? JSON.parse(prediction?.outputs_json)
    : null;

  const target = outputs_json?.model_metadata.target ?? "y_pred";
  const X = outputs_json?.X as Array<Record<string, unknown>>;
  const featureColumnNames = X?.length > 0 ? Object.keys(X[0]) : [];
  const columnNames = [...featureColumnNames, target];
  const rows =
    X?.length > 0
      ? X.map((row, i) => ({
          ...row,
          [target]: outputs_json.y_pred[i],
        }))
      : null;

  if (loading) {
    return <Loading />;
  }

  if (!prediction) return <NotFound name="Prediction" />;
  if (!rows) return <NotFound bypass="Prediction could not be read." />;

  return (
    <div className="w-full pl-4 pt-8">
      <div className="mx-auto w-full px-6">
        <h1>Prediction: {prediction?.name ?? "Unknown Prediction"}</h1>
        <p className="mt-1 mb-4 text-sm text-muted-foreground">
          Results and details for {prediction?.name ?? "Unknown Prediction"}.
        </p>
        <PredictionTable columnNames={columnNames} rows={rows} />
        <div className="mt-2 grid grid-cols-3 items-center">
          <div />
          {/* {totalPages > 1 ? (
            <div className="flex justify-center">
              <Pagination totalPages={totalPages} />
            </div>
          ) : (
            <div />
          )} */}
          <div className="flex justify-end">
            <PageSize size={size} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictionDetailPage;
