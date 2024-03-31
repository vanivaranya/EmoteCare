function toggleSubsections(section) {
  section.classList.toggle('clicked');
  const subsections = section.querySelector('.subsections');
  if (subsections.style.display === 'flex') {
      subsections.style.display = 'none'; // Close if already open
  } else {
      subsections.style.display = 'flex';
  }
}