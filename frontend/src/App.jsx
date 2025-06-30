// import {useState, useEffect} from 'react';
// import {BrowserRouter, Routes, Route} from 'react-router-dom';
//import Axios from './services/Axios';
// import NavigationBar from './components/NavigationBar';
import {Route, createBrowserRouter, RouterProvider, createRoutesFromElements} from 'react-router-dom';
import AddStudentPage from './pages/AddStudentPage';



const App = () => {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        <Route path="/" element={<div>Home Page</div>}/>
        <Route path='add-student' element={<AddStudentPage/>} />
      </>
    )
  );

  return (
    <RouterProvider router={router} />
  );


}

export default App