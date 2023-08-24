import React, {useContext, useState, useEffect} from 'react';
import useAxios from "../../../utils/useAxios";
import AuthContext from "../../../context/AuthContext";

function ProfilePage() {
  const api = useAxios();
  const {user} = useContext(AuthContext);
  const [profile, setProfile] = useState(null);


  async function fetchProfile() {
    let response = await api.get(`api/v1/profile/${user.user_id}/`);
    if (response.status === 200){
      return response.data;
    }
  }

  useEffect(() => {
    fetchProfile().then(response => {

      setProfile(response);
      console.log(response)
    })
    ;
  }, [])


  if (profile) {
    return (
        <div>
          {profile.profile_image &&
              <div>
                <img
                  src={
                    profile.profile_image.indexOf('http') === -1
                      ? 'http://127.0.0.1:8000' + profile.profile_image
                      : profile.profile_image
                  }
                  className="img-fluid mh-100 w-auto p-3" alt=""
                />
              </div>
          }
          <div>Username: {profile.username}</div>
          {/*{profile.email ? <p>Email: {profile.email}</p> : <></>}*/}
          {profile.first_name && <div>First Name: {profile.first_name}</div> }
          {profile.last_name && <div>Last Name: {profile.last_name}</div> }
          {profile.bio && <div>Bio: {profile.bio }</div>}
        </div>
    );
  }
  else {
    return (<></>)
  }
}

export default ProfilePage;