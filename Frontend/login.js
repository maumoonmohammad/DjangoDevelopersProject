let form = document.getElementById('login-form')

form.addEventListener('submit', (e) => {
    e.preventDefault() //prevents the page from refreshing

    let formData = {
        'username': form.username.value,
        'password': form.password.value
    }

    console.log(formData)


    fetch('http://127.0.0.1:8000/api/users/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
        .then(resposne => resposne.json())
        .then(data => {
            console.log(data.access)
            if (data.access) {
                localStorage.setItem('token', data.access)
                window.location = 'file:///Users/maumoonmohammad/Desktop/DevSearch%20Frontend/projects-list.html'
            } else {
                alert('Username or Password did not work')
            }

        })
})