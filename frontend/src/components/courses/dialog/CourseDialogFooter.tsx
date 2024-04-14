import { useCoursesContext } from "../../../contexts/CoursesContext";
import { useCourseDialogContext } from "../../../contexts/CourseDialogContext";
import React from "react";

export default function CourseDialogFooter() {
  const { course, variant } = useCourseDialogContext();
  const { updateCourse, addCourse } = useCoursesContext();

  const handleUpdate = () => {
    console.log("sending this to backend for updating: ", course);
    updateCourse(course.id, course);
  };

  const handleAdd = () => {
    console.log("sending this to backend for adding: ", course);
    addCourse(course);
  };

  const handleSubmit = () => {
    // validate using zod
    const action = variant === "new" ? handleAdd : handleUpdate;
    action();
  };

  const acceptButtonText =
    variant === "new" ? "Dodaj przedmiot" : "Edytuj przedmiot";

  return (
    <div className="ml-auto flex items-center gap-4">
      <button className="py-2 px-4 bg-slate-600 text-white text-sm hover:bg-slate-800 rounded-sm">
        Anuluj
      </button>
      <button
        onClick={handleSubmit}
        className="py-2 px-4 bg-blue-500 text-white text-sm hover:bg-blue-600 rounded-sm"
      >
        {acceptButtonText}
      </button>
    </div>
  );
}
