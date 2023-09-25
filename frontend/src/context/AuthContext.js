import React, {createContext, useEffect, useState} from 'react'
import jwt_decode from "jwt-decode"
import {useNavigate} from "react-router-dom"


const AuthContext = createContext(undefined)
export default AuthContext


export const AuthProvider = ({children}) => {
    const navigate = useNavigate()
    const [accessToken, setAccessToken] = useState(() => localStorage.getItem('accessToken'))
    const [refreshToken, setRefreshToken] = useState(() => localStorage.getItem('refreshToken'))
    const [user, setUser] = useState(() => localStorage.getItem('accessToken') ? jwt_decode(localStorage.getItem('accessToken')) : null)
    
    const [loading, setLoading] = useState(true)


    async function loginUser(username, password){
        const response =  await fetch('http://localhost:8000/api/v1/token/',
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                },
              body: JSON.stringify({'username': username, 'password': password})
            }
        )

        const response_status = response.status
        const response_data = await response.json()

        if (response_status === 200){
            setAccessToken(response_data.access)
            setRefreshToken(response_data.refresh)
            setUser(jwt_decode(response_data.access))

            localStorage.setItem('accessToken', response_data.access)
            localStorage.setItem('refreshToken', response_data.refresh)
        }
        return [response_status, response_data]
    }



    async function signUpUser(username, password){
        let response =  await fetch('http://localhost:8000/api/v1/user/signup/',
            {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                },
            body: JSON.stringify({'username': username, 'password': password})
            }
        )
        let response_status = response.status
        let response_data = await response.json()

        return [response_status, response_data]
      }

    

    function logoutUser(){
        setAccessToken(null)
        setRefreshToken(null)
        setUser(null)

        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        navigate('/login')
    }


    async function updateToken(){
        console.log('Update token')
        if (refreshToken){
            let response =  await fetch('http://localhost:8000/api/v1/token/refresh/',
                {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({'refresh': refreshToken})
            })
            
            let data = await response.json()
            if (response.status === 200){
                setAccessToken(data.access)
                setUser(jwt_decode(data.access))
                localStorage.setItem('accessToken', accessToken)
            }
            else {
                logoutUser()
            }
        }
        setLoading(false)
    }
   

    // not the best practice
    useEffect(() => {
        if(loading){
            updateToken()
        }

        const fourMinutes = 4 * 60 * 1000
        const interval = setInterval(()=> {
            if (refreshToken){
                updateToken()
            }

        }, fourMinutes)
        return ()=> clearInterval(interval)

    }, [accessToken, loading])


    const contextData = {
        user: user,
        accessToken: accessToken,
        loginUser: loginUser,
        signUpUser: signUpUser,
        logoutUser:logoutUser,
    }

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    )
}
