import {useContext} from "react"
import AuthContext from "../context/AuthContext"

function PrivateRoute(children){
    const {user, logoutUser} = useContext(AuthContext)
    if (!user){
        return logoutUser()
    }
    return children
}

export default PrivateRoute