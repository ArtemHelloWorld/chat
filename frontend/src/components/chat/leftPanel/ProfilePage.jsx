import React, {useContext, useEffect, useState} from "react"
import useAxios from "../../../utils/useAxios"
import AuthContext from "../../../context/AuthContext"

function ProfilePage() {
  const api = useAxios()
  const {user} = useContext(AuthContext)
  const [profile, setProfile] = useState(null)


  async function fetchProfile() {
    const response = await api.get(`api/v1/profile/${user.user_id}/`)
    if (response.status === 200){
      return response.data
    }
  }

  function wrapIntoBox(title, value)  {
     return(
       <div className="d-flex justify-content-start mx-3">
         <div className="px-3 border">{title}</div>
         <div className="px-3 flex-grow-1 border">{value}</div>
       </div>
     )
  }

  useEffect(() => {
    fetchProfile().then(response => {
      setProfile(response)
      console.log(response)
    })
  }, [])


  if (profile){
    return (
        <div>
          {profile.profile_image &&
              <div>
                <img
                  src={
                    profile.profile_image.indexOf("http") === -1
                      ? "http://127.0.0.1:8000" + profile.profile_image
                      : profile.profile_image
                  }
                  className="img-fluid mh-100 w-auto p-3" alt=""
                />
              </div>
          }

          {wrapIntoBox("Username", profile.username)}
          {profile.first_name && wrapIntoBox("First name", profile.first_name)}
          {profile.last_name && wrapIntoBox("Last name", profile.last_name)}
          {profile.bio && wrapIntoBox("Bio", profile.bio)}
        </div>
    )
  }
  else {
    return <></>
  }
}

export default ProfilePage