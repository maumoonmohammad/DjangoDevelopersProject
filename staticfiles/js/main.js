
// GET SEARCH FORM AND PAGE LINKS
let searchForm = document.getElementById('searchForm')
let pagelinks = document.getElementsByClassName('page-link')

// ENSURE SEARCH FORM EXISTS

if (searchForm) {
    for (let i = 0; pagelinks.length > i; i++) {
        pagelinks[i].addEventListener('click', function (e) {
            e.preventDefault()

            //GET THE DATA ATTRIBUTR
            let page = this.dataset.page
            console.log('PAGE:', page)

            // ADD HIDDEN SEARCH INPUT TO FORM

            searchForm.innerHTML += `<input value=${page} name="page" hidden/>`

            // SUBMIT FORM

            searchForm.submit()
        })
    }


}


let tags = document.getElementsByClassName('project-tag')

for (let i = 0; i < tags.length; i++) {
    tags[i].addEventListener('click', (e) => {
        e.preventDefault()
        let tagId = e.target.dataset.tag
        let projectId = e.target.dataset.project
        // console.log('TAG ID:', tagId)
        // console.log('Project ID:', projectId)

        fetch('http://127.0.0.1:8000/api/remove-tag/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'

            },
            body: JSON.stringify({ 'project': projectId, 'tag': tagId })
        })
            .then(resposne => resposne.json())
            .then(data => {
                e.target.remove()
            })
    })
}


