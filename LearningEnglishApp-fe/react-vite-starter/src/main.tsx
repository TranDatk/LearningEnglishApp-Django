import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import {
  createBrowserRouter,
  Outlet,
  RouterProvider,
} from "react-router-dom";
import UsersPage from './screens/users.page.tsx';
import Header from './components/users/header.tsx';

const LayoutAdmin = () => {
  return (
    <div>
      <Header />
      <Outlet />
      <footer>Footer</footer>
    </div>
  )
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <LayoutAdmin />,
    children: [
      {
        index: true,
        element: <App />,
      },
      {
        path: "users",
        element: <UsersPage />,
      },
    ]
  },

]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
