// import {useState, useEffect} from 'react';
// import {BrowserRouter, Routes, Route} from 'react-router-dom';
//import Axios from './services/Axios';
// import NavigationBar from './components/NavigationBar';

import {Route, createBrowserRouter, RouterProvider, createRoutesFromElements} from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import HomePage from './pages/HomePage';
import AddStudentPage from './pages/AddStudentPage';
import NotFoundPage from './pages/NotFoundPage';
import StudentRecordsPage from './pages/StudentRecordsPage';
import AddStudentCoursePage from './pages/AddStudentCoursePage';


const App = () => {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path="/" element={<MainLayout/>}>
        <Route index element={<HomePage />} />
        <Route path='/add-student' element={<AddStudentPage/>} />  
        
        <Route path='/student-records' element={<StudentRecordsPage />} />
        <Route path='/add-student-course' element={<AddStudentCoursePage />} />
        <Route path='*' element={<NotFoundPage />} />
      </Route>
    )
  );

  return (
    <RouterProvider router={router} />
  );


}

export default App