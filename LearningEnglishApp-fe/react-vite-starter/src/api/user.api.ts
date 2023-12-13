/** @format */

import cookies from "react-cookies";
import { client_id, client_secret } from "../constants/user.constants";
import { BASE_URL, endpoints } from "./api";

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

export const AuthAPI = async () => {
    const res = await fetch(BASE_URL, {
      method: "GET",
      headers: {
        'Authorization':`Bearer ${cookies.load('access_token')}`
      },
    });
    const data = await res.json();
    return data;
  };