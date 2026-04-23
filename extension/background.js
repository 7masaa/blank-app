chrome.commands.onCommand.addListener(async (command) => {
  const tabMap = {
    open_extension: 'account',
    open_snippets: 'snippets',
    open_tickets: 'tickets',
    open_resources: 'resources'
  };

  const targetTab = tabMap[command];
  if (!targetTab) return;

  await chrome.storage.local.set({ preferredTab: targetTab });
  chrome.action.openPopup();
});
