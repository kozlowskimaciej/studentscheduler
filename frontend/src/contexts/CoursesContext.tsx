import React, { createContext, useContext, useState } from "react";
import { Course } from "../models/Course";

type CoursesContextType = {
  courses: Course[];
  setCourses: React.Dispatch<React.SetStateAction<Course[]>>;
  removeCourse: (id: string) => void;
  updateCourse: (id: string, newCourse: Course) => void;
  addCourse: (course: Course) => void;
};

const CoursesContext = createContext<CoursesContextType>(
  {} as CoursesContextType
);

export const useCoursesContext = () => useContext(CoursesContext);

export const CoursesContextProvider = ({
  children,
  courses: initCourses,
}: {
  children: React.ReactNode;
  courses: Course[];
}) => {
  const [courses, setCourses] = useState(initCourses);

  const removeCourse = (id: string): void => {
    setCourses((prev) => prev.filter((course) => course.id !== id));
  };

  const updateCourse = (id: string, newCourse: Course): void => {
    setCourses((prev) => {
      const idx = prev.findIndex((course) => course.id === id);
      const updatedCourses = [
        ...prev.slice(0, idx),
        newCourse,
        ...prev.slice(idx + 1),
      ];
      return updatedCourses;
    });
  };

  const addCourse = (course: Course): void => {
    setCourses((prev) => [...prev, course]);
  };

  return (
    <CoursesContext.Provider
      value={{
        courses,
        setCourses,
        removeCourse,
        updateCourse,
        addCourse,
      }}
    >
      {children}
    </CoursesContext.Provider>
  );
};
