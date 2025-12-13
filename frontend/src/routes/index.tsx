import { createBrowserRouter } from "react-router-dom";
import AppPage from "../pages/app/AppPage";
import DashboardLayout from "../layouts/dashboard/DashboardLayout";
import DashboardPage from "../pages/dashboard/DashboardPage";
import DatasetsPage from "../pages/dashboard/datasets/DatasetsPage";
import JobsPage from "../pages/dashboard/jobs/JobsPage";
import DatasetIdPage from "../pages/dashboard/datasets/DatasetIdPage";
import DatasetVersionIdPage from "../pages/dashboard/dataset_versions/DatasetVersionIdPage";
import MLProblemIdPage from "../pages/dashboard/ml_problems/MLProblemIdPage";
import ModelIdPage from "@/pages/dashboard/models/ModelIdPage";

export const router = createBrowserRouter([
  { path: "/", element: <AppPage /> },
  {
    path: "/dashboard",
    element: <DashboardLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: "datasets", element: <DatasetsPage /> },
      { path: "datasets/:datasetId", element: <DatasetIdPage /> },
      {
        path: "datasets/:datasetId/:datasetVersionId",
        element: <DatasetVersionIdPage />,
      },
      {
        path: "datasets/:datasetId/:datasetVersionId/:problemId",
        element: <MLProblemIdPage />,
      },
      {
        path: "datasets/:datasetId/:datasetVersionId/:problemId/:modelId",
        element: <ModelIdPage />,
      },
      { path: "jobs", element: <JobsPage /> },
    ],
  },
]);
