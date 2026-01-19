import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Ellipsis, FileText, Edit, Trash2, Copy } from "lucide-react";
import { Link } from "react-router-dom";
import { toast } from "sonner";

type Props = {
  datasetId: string;
  datasetVersionId: string;
  problemId: string;
  modelId: string;
  parent: string;
  onDelete: () => void;
  onUpdate: () => void;
};

const ModelActions = ({
  datasetId,
  datasetVersionId,
  problemId,
  modelId,
  parent,
  onDelete,
  onUpdate,
}: Props) => {
  const viewUrl = `/dashboard/datasets/${datasetId}/${datasetVersionId}/${problemId}`;

  return (
    <div className="flex items-center justify-start gap-1.5">
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <Link
              to={viewUrl}
              aria-label={"View " + parent}
              className="inline-flex items-center justify-center text-muted-foreground hover:text-sky-400 hover:scale-105 active:scale-95"
            >
              <FileText className="w-4 h-4" />
            </Link>
          </TooltipTrigger>
          <TooltipContent>View {parent}</TooltipContent>
        </Tooltip>
        <Tooltip>
          <TooltipTrigger asChild>
            <button
              onClick={() => {
                navigator.clipboard.writeText(modelId);
                toast.success("Model id copied to clipboard");
              }}
              className="text-muted-foreground hover:text-sky-400 hover:scale-105 active:scale-95"
              aria-label="Copy model id"
              type="button"
            >
              <Copy className="w-4 h-4" />
            </button>
          </TooltipTrigger>
          <TooltipContent>Copy model id</TooltipContent>
        </Tooltip>
        <DropdownMenu>
          <DropdownMenuTrigger className="text-muted-foreground hover:text-sky-400 hover:scale-105 active:scale-95 focus-visible:outline-none">
            <Tooltip>
              <TooltipTrigger asChild>
                <Ellipsis className="w-4 h-4" />
              </TooltipTrigger>
              <TooltipContent>More Actions</TooltipContent>
            </Tooltip>
          </DropdownMenuTrigger>

          <DropdownMenuContent>
            <Link to={viewUrl}>
              <DropdownMenuItem className="group text-muted-foreground">
                <FileText className="w-4 h-4 group-data-[highlighted]:text-sky-400" />
                View (Problem)
              </DropdownMenuItem>
            </Link>

            <DropdownMenuItem
              onClick={() => {
                navigator.clipboard.writeText(datasetId);
                toast.success("Dataset id copied to clipboard");
              }}
              className="group text-muted-foreground"
            >
              <Copy className="w-4 h-4 group-data-[highlighted]:text-sky-400" />
              Copy dataset id
            </DropdownMenuItem>

            <DropdownMenuItem
              onClick={() => {
                navigator.clipboard.writeText(datasetVersionId);
                toast.success("Dataset version id copied to clipboard");
              }}
              className="group text-muted-foreground"
            >
              <Copy className="w-4 h-4 group-data-[highlighted]:text-sky-400" />
              Copy dataset version id
            </DropdownMenuItem>

            <DropdownMenuItem
              onClick={() => {
                navigator.clipboard.writeText(problemId);
                toast.success("ML problem id copied to clipboard");
              }}
              className="group text-muted-foreground"
            >
              <Copy className="w-4 h-4 group-data-[highlighted]:text-sky-400" />
              Copy ML problem id
            </DropdownMenuItem>

            <DropdownMenuItem
              onClick={() => {
                navigator.clipboard.writeText(modelId);
                toast.success("Model id copied to clipboard");
              }}
              className="group text-muted-foreground"
            >
              <Copy className="w-4 h-4 group-data-[highlighted]:text-sky-400" />
              Copy model id
            </DropdownMenuItem>

            <DropdownMenuItem
              onClick={onUpdate}
              className="group text-muted-foreground"
            >
              <Edit className="w-4 h-4 group-data-[highlighted]:text-sky-400" />
              Edit
            </DropdownMenuItem>

            <DropdownMenuItem
              onClick={onDelete}
              className="group text-muted-foreground"
            >
              <Trash2 className="w-4 h-4 group-data-[highlighted]:text-red-500" />
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </TooltipProvider>
    </div>
  );
};

export default ModelActions;
