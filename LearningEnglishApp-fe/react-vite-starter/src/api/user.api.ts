/** @format */

import cookies from "react-cookies";
import { client_id, client_secret } from "../constants/user.constants";
import { BASE_URL, endpoints } from "./api";
import { IUser } from "../components/users/user.table";
import API from './api';


export const login = async (username: string, password: string) => {
  const res = await fetch(BASE_URL + endpoints["login"], {
    method: "POST",
    body: JSON.stringify({
      username: username,
      password: password,
      client_id: client_id,
      client_secret: client_secret,
      grant_type: "password",
    }),
  });
  const data = await res.json();
  cookies.save("access_token", data.access_token, { path: "/" });
};

export const getListUsers = async (currentPage : number) => {
  try {
    const userList = await API.get(`${endpoints["users"]}?page=${currentPage}`);
    return userList;
  } catch (error) {
    console.error("Đã xảy ra lỗi khi lấy danh sách người dùng:", error);
    throw error; 
  }
};

export const registerUser = async (user: IUser) => {
  try {
    const res = await API.post(endpoints["register"], {
      username: user.username,
      password1: user.password1,
      password2: user.password2,
      email: user.email,
      first_name: user.first_name,
      last_name: user.last_name,
      // avatar: user?.avatar[0]?.originFileObj,
      is_superuser: user.is_superuser
    }, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return res; 

  } catch (error) {
    console.error("Đã xảy ra lỗi khi đăng ký người dùng:", error);
    throw error;
  }
};

export const updateUser = async (user: IUser) => {
  try {
    const res = await API.patch(endpoints["updateUser"], {
      id: user.id,
      username: user.username,
      email: user.email,
      first_name: user.first_name,
      last_name: user.last_name,
      is_superuser: user.is_superuser
    }, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return res; 

  } catch (error) {
    console.error("Đã xảy ra lỗi khi sửa thông tin người dùng:", error);
    throw error;
  }
};

export const hideUser = async (id: number) => {
  try {
    const res = await API.post(endpoints["users"] + `${id}/hide-user/`, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    return res; 

  } catch (error) {
    console.error("Đã xảy ra lỗi khi ẩn người dùng:", error);
    throw error;
  }
};