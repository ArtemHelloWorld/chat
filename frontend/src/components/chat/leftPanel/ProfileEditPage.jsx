import React, {useContext, useState, useEffect} from 'react';
import useAxios from "../../../utils/useAxios";
import AuthContext from "../../../context/AuthContext";
import {MdOutlineAddAPhoto} from 'react-icons/md';


function ProfileEditPage({setActivePanel}) {
  const api = useAxios();
  const {user} = useContext(AuthContext);
  const [profile, setProfile] = useState(null);
  const [newPhotoUploaded, setNewPhotoUploaded] = useState(false);
  const [formData, setFormData] = useState({});

  async function fetchUser() {
    let response = await api.get(`api/v1/user/${user.user_id}/`);
    if (response.status === 200){
      return response.data;
    }
  }

  useEffect(() => {
    fetchUser().then(response => {
      setProfile(response);
      setFormData(response);
      console.log(response);
    })
    ;
  }, [])

  const handleChange = event => {
      const { name, value } = event.target;
      setFormData({
          ...formData,
          [name]: value,
      });
  };

  const handlePhotoChange = event => {

    console.log(event)
      setFormData({
          ...formData,
          profile_image: event.target.files[0],
      });
    setNewPhotoUploaded(true)
  };
  const handleSubmit = event => {
      event.preventDefault();
      const formDataToSend = new FormData();
      for (const key in formData) {
          if (formData[key] !== profile[key]){
            formDataToSend.append(key, formData[key]);
          }
      }

      api.patch(`/api/v1/user/${user.user_id}/`, formDataToSend
      ).then(response => {
          setActivePanel('profile')
      })
      .catch(error => {
          // todo: handle error
      });
  };

  if (formData) {
    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div>
                  {(formData.profile_image ||newPhotoUploaded ) &&
                    <img
                      src={newPhotoUploaded ?
                            URL.createObjectURL(formData.profile_image)
                                :
                            (profile.profile_image.indexOf('http') === -1 ?
                                'http://127.0.0.1:8000' + profile.profile_image
                                : profile.profile_image
                            )
                      }
                      className="img-fluid mh-100 w-auto p-3 pb-1" alt=""
                    />
                  }
                </div>
                <div>
                  <label onChange={handlePhotoChange} htmlFor="image">
                    <input type="file" accept="image/*" placeholder="Фото" name="profile_photo" id="image" hidden/>
                   <MdOutlineAddAPhoto size="3rem"/>
                  </label>
                </div>
                {/*<input type="email" placeholder="Биография" name="email" value={formData.email} onChange={handleChange} />*/}
                <div><input type="text" placeholder="Имя" name="first_name" value={formData.first_name || ''} onChange={handleChange} /></div>
                <div><input type="text" placeholder="Фамилия" name="last_name" value={formData.last_name || ''} onChange={handleChange} /></div>
                <div><input type="text" placeholder="Биография" name="biography" value={formData.bio || ''} onChange={handleChange} /></div>
                <div><button type="submit">Сохранить изменения</button></div>
            </form>
        </div>
    );
  }
  else {
    return (<>dfd</>)
  }
}

export default ProfileEditPage;