import { useState } from "react";
import { Button } from "../ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogOverlay,
  DialogTitle,
} from "../ui/dialog";
import { Input } from "../ui/input";
import { Label } from "../ui/label";

type DatasetDeleteProps = {
  target: { id: string; name: string };
  open: boolean;
  onOpenChange: (v: boolean) => void;
};

export type DeleteTarget = {
  id: string;
  name: string;
};

const DatasetDelete = ({ target, open, onOpenChange }: DatasetDeleteProps) => {
  const [confirmText, setConfirmText] = useState("");
  const canDelete = confirmText.trim().toLowerCase() === "delete";

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <form>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Delete Dataset</DialogTitle>
            <div className="text-sm">
              Are you sure you want to delete dataset: <b>{target.name}?</b>
            </div>
            <div className="text-muted-foreground text-sm">
              <i>id: {target.id}</i>
            </div>
            <div className="text-sm">
              Deleting this dataset will permanently delete all associated
              versions, problems, and models.
            </div>
          </DialogHeader>
          <div className="grid gap-4">
            <div className="grid gap-3">
              <Label htmlFor="name-1">Type "delete" to confirm</Label>
              <Input
                id="delete"
                name="delete"
                value={confirmText}
                onChange={(e) => setConfirmText(e.target.value)}
              />
            </div>
          </div>
          <DialogFooter>
            <DialogClose asChild>
              <Button variant="outline">Cancel</Button>
            </DialogClose>
            <Button variant="destructive" disabled={!canDelete}>
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </form>
      <DialogOverlay className="bg-black/30 backdrop-blur-sm" />
    </Dialog>
  );
};

export default DatasetDelete;
