const tabs = document.querySelectorAll('nav button');
const sections = document.querySelectorAll('.tab');

function selectTab(tabName) {
  tabs.forEach((btn) => btn.classList.toggle('active', btn.dataset.tab === tabName));
  sections.forEach((section) => section.classList.toggle('active', section.id === tabName));
}

tabs.forEach((btn) => btn.addEventListener('click', () => selectTab(btn.dataset.tab)));

chrome.storage.local.get(['preferredTab'], ({ preferredTab }) => {
  selectTab(preferredTab || 'account');
});
