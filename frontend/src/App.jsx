// import {useState, useEffect} from 'react';
// import {BrowserRouter, Routes, Route} from 'react-router-dom';
//import Axios from './services/Axios';
// import NavigationBar from './components/NavigationBar';

import {Route, createBrowserRouter, RouterProvider, createRoutesFromElements} from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import HomePage from './pages/HomePage';
import AddStudentPage from './pages/AddStudentPage';



const App = () => {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path="/" element={<MainLayout/>}>
        <Route index elemet={<HomePage />} />
        <Route path='/add-student' element={<AddStudentPage/>} />   
      </Route>
    )
  );

  return (
    <RouterProvider router={router} />
  );


}

export default App