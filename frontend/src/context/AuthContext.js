import React, {createContext, useState, useEffect} from 'react';
import jwt_decode from "jwt-decode";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();
export default AuthContext;


export const AuthProvider = ({children}) => {
    let [accessToken, setAccessToken] = useState(() => localStorage.getItem('accessToken'));
    let [refreshToken, setRefreshToken] = useState(() => localStorage.getItem('refreshToken'));
    let [user, setUser] = useState(() => localStorage.getItem('accessToken') ? jwt_decode(localStorage.getItem('accessToken')) : null);
    
    let [loading, setLoading] = useState(true);
    let navigate = useNavigate();

    
    let loginUser = async (event) =>  {
        event.preventDefault();
        let response =  await fetch('http://localhost:8000/api/v1/token/',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            },
          body: JSON.stringify({'username': event.target.username.value, 'password': event.target.password.value})
        });
        
        let data = await response.json();
        console.log(data);

        if (response.status === 200){
            setAccessToken(data.access);
            setRefreshToken(data.refresh);
            setUser(jwt_decode(data.access));

            localStorage.setItem('accessToken', data.access);
            localStorage.setItem('refreshToken', data.refresh);

            navigate('/');
        }
        else {
            alert('somethin went wrong');
        }
    }

    let logoutUser = () => {
        setAccessToken(null);
        setRefreshToken(null);
        setUser(null);

        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');

        navigate('/login');
    }


    let updateToken = async () => {
        console.log('Update token')
        if (refreshToken){
            let response =  await fetch('http://localhost:8000/api/v1/token/refresh/',
                {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({'refresh': refreshToken})
            });
            
            let data = await response.json();
            if (response.status === 200){
                setAccessToken(data.access);
                setUser(jwt_decode(data.access));

                localStorage.setItem('accessToken', accessToken);
            }
            else {
                logoutUser();
            }
        }
        setLoading(false);
    }


    let contextData = {
        user: user,
        accessToken: accessToken,
        loginUser: loginUser,
        logoutUser:logoutUser,
    }

    // not the best practice
    useEffect(() => {
        if(loading){
            updateToken();
        }

        let fourMinutes = 4 * 60 * 1000

        let interval =  setInterval(()=> {
            if (refreshToken){
                updateToken();
            }
            
        }, fourMinutes);
        return ()=> clearInterval(interval);

    }, [accessToken, loading])

    
    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    )
}
