import { createBrowserRouter } from "react-router-dom";
import AppPage from "../pages/app/AppPage";
import DashboardLayout from "../layouts/dashboard/DashboardLayout";
import DashboardPage from "../pages/dashboard/DashboardPage";
import DatasetsPage from "../pages/dashboard/datasets/DatasetsPage";
import JobsPage from "../pages/dashboard/jobs/JobsPage";
import DatasetDetailPage from "../pages/dashboard/datasets/DatasetDetailPage";

export const router = createBrowserRouter([
  { path: "/", element: <AppPage /> },
  {
    path: "/dashboard",
    element: <DashboardLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: "datasets", element: <DatasetsPage /> },
      { path: "datasets/:datasetId", element: <DatasetDetailPage /> },
      { path: "jobs", element: <JobsPage /> },
    ],
  },
]);
