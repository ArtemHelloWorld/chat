import axios from "axios";
import {useContext} from "react";
// import jwt_decode from "jwt-decode";
import AuthContext from "../context/AuthContext";


const baseURL = "http://127.0.0.1:8000/"




const useAxios = () => {
    const {accessToken} = useContext(AuthContext);
    
    const AxiosInstance = axios.create({
      baseURL, 
      headers: {
          // 'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`
      }
    })
   
    // async function refreshAccessToken() {
    //   if (refreshToken){
    //     const response = await axios.post(`${baseURL}api/v1/token/refresh/`, {
    //       refresh: refreshToken
    //     })
    //     console.log(response.status)
    //     if (response.status === 200){
    //       console.log(response.data.access)
    //       return response.data.access;
    //     }
    //     else {
    //         logoutUser();
    //         return null;
    //     }
    //   }
    // }


    

    // AxiosInstance.interceptors.response.use(
    //     (response) => {
    //       console.log('response(((')
    //         return response;

    //       },
    //       async (error) => {
    //         console.log('expired')
    //         const originalRequest = error.config;
        
    //         if (error.response.status === 401 && !originalRequest._retry) {
    //           originalRequest._retry = true;
              
    //             const newToken = await refreshAccessToken(); 
    //             console.log(newToken, 'newToken')
    //             if (newToken) {
    //               originalRequest.headers.Authorization = `Bearer ${newToken}`;
    //               setAccessToken(newToken);
    //               setUser(jwt_decode(newToken));
    //               localStorage.setItem('accessToken', newToken);
  
          
    //               return AxiosInstance(originalRequest);
    //             }
    //           }
    //         return Promise.reject(error);
    //     }
    // )
    
    return AxiosInstance;
}

export default useAxios;
