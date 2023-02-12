const tabs = document.querySelectorAll('[data-tab-target]')
const tabcontents = document.querySelectorAll('[data-tab-content]')
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const target = document.querySelector(tab.dataset.tabTarget)
        tabcontents.forEach(tabcontent  => {
            tabcontent.classList.remove('active')
        })
        tabs.forEach(tab  => {
            tab.classList.remove('active')
        })
        tab.classList.add('active')
        target.classList.add('active')
    })
})