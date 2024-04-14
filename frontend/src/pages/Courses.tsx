import React from "react";
import Navbar from "../components/common/Navbar";
import Footer from "../components/common/Footer";
import CoursesAccordion from "../components/courses/accordion/CoursesAccordion";
import { CoursesContextProvider } from "../contexts/CoursesContext";
import { coursesFakeData } from "../api/Courses";
import NewCourseDialog from "../components/courses/NewCourseDialog";

export default function Courses() {
  return (
    <CoursesContextProvider courses={coursesFakeData}>
      <Navbar />
      <CoursesAccordion />
      <NewCourseDialog />
      <Footer />
    </CoursesContextProvider>
  );
}
