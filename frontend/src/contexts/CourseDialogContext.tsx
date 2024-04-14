import React, { createContext, useContext, useEffect, useState } from "react";
import { Course } from "../models/Course";
import { Requirement } from "../models/Requirement";
import { Task } from "../models/Task";

type CourseDialogContextType = {
  course: Course;
  setCourse: React.Dispatch<React.SetStateAction<Course>>;
  removeRequirement: (id: number) => void;
  updateRequirement: (id: number, field: string, val: any) => void;
  addEmptyRequirement: () => void;
  removeTask: (id: number) => void;
  updateTask: (id: number, field: string, val: any) => void;
  addEmptyTask: () => void;
  variant: CourseDialogVariantType;
};

export type CourseDialogVariantType = "new" | "edit";

const CourseDialogContext = createContext<CourseDialogContextType>(
  {} as CourseDialogContextType
);

export const useCourseDialogContext = () => useContext(CourseDialogContext);

export const CourseDialogContextProvider = ({
  children,
  course: initCourse,
  variant,
}: {
  children: React.ReactNode;
  course: Course;
  variant: CourseDialogVariantType;
}) => {
  const [course, setCourse] = useState(initCourse);

  useEffect(() => {
    console.log(course);
  }, [course]);

  const removeRequirement = (id: number): void => {
    setCourse((prev) => {
      const filteredRequirements = prev.requirements.filter(
        (_, idx) => id !== idx
      );
      const newCourse: Course = {
        ...course,
        requirements: filteredRequirements,
      };
      return newCourse;
    });
  };

  const updateRequirement = (id: number, field: string, val: any): void => {
    const updatedReq = course.requirements.find(
      (_, idx) => id === idx
    )! as any;
    updatedReq[field] = val;
    setCourse((prev) => ({ ...prev }));
  };

  const addEmptyRequirement = (): void => {
    const newRequirement: Requirement = {
      task_type: "Laboratorium",
      requirement_type: "Total",
      threshold: 0,
      threshold_type: "Points",
    };
    const requirements = [...course.requirements, newRequirement];
    setCourse((prev) => ({ ...prev, requirements }));
  };

  const removeTask = (id: number): void => {
    setCourse((prev) => {
      const filteredTasks = prev.tasks.filter((_, idx) => id !== idx);
      const newCourse: Course = {
        ...course,
        tasks: filteredTasks,
      };
      return newCourse;
    });
  };

  const updateTask = (id: number, field: string, val: any): void => {
    const updatedTask = course.tasks.find((_, idx) => id === idx)! as any;
    updatedTask[field] = val;
    setCourse((prev) => ({ ...prev }));
  };

  const addEmptyTask = (): void => {
    const newTask: Task = {
      max_points: 0,
      result: null,
      deadline: new Date(),
      task_type: "Laboratorium",
      description: "",
    };
    const tasks = [...course.tasks, newTask];
    setCourse((prev) => ({ ...prev, tasks }));
  };

  return (
    <CourseDialogContext.Provider
      value={{
        course,
        setCourse,
        removeRequirement,
        updateRequirement,
        addEmptyRequirement,
        removeTask,
        updateTask,
        addEmptyTask,
        variant,
      }}
    >
      {children}
    </CourseDialogContext.Provider>
  );
};
