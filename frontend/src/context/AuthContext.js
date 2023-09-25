import React, {createContext, useState, useEffect} from 'react'
import jwt_decode from "jwt-decode"
import {useNavigate} from "react-router-dom"


const AuthContext = createContext(undefined)
export default AuthContext


export const AuthProvider = ({children}) => {
    let navigate = useNavigate()
    let [accessToken, setAccessToken] = useState(() => localStorage.getItem('accessToken'))
    let [refreshToken, setRefreshToken] = useState(() => localStorage.getItem('refreshToken'))
    let [user, setUser] = useState(() => localStorage.getItem('accessToken') ? jwt_decode(localStorage.getItem('accessToken')) : null)
    
    let [loading, setLoading] = useState(true)


    const loginUser = async (username, password) =>  {


        let response =  await fetch('http://localhost:8000/api/v1/token/',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            },
          body: JSON.stringify({'username': username, 'password': password})
        })

        let response_status = response.status
        let response_data = await response.json()

        if (response_status === 200){
            setAccessToken(response_data.access)
            setRefreshToken(response_data.refresh)
            setUser(jwt_decode(response_data.access))

            localStorage.setItem('accessToken', response_data.access)
            localStorage.setItem('refreshToken', response_data.refresh)
        }
        return [response_status, response_data]
    }



    const signUpUser = async (username, password) =>  {
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

    

    let logoutUser = () => {
        setAccessToken(null)
        setRefreshToken(null)
        setUser(null)

        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        console.log('navigate')
        navigate('/login')
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
            })
            
            let data = await response.json()
            console.log(data)
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

        let fourMinutes = 4 * 60 * 1000

        let interval =  setInterval(()=> {
            if (refreshToken){
                updateToken()
            }
            
        }, fourMinutes)
        return ()=> clearInterval(interval)

    }, [accessToken, loading])


    let contextData = {
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
