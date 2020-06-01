document.addEventListener("DOMContentLoaded", () => {

    const getTonalityBtn = document.getElementsByClassName('getTonality')
    const getFactsBtn = document.getElementsByClassName('getFacts')

    for(const btn of getTonalityBtn) {
        btn.addEventListener('click', async (event) => {
            const articleId = event.target.dataset.id
            const res = await fetch(`/getTonality/${articleId}`)
            const tonality = await res.json()

        })
    }


})