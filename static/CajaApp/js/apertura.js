  document.addEventListener('DOMContentLoaded', (event) => {
      const now = new Date();
      const formattedDate = now.toISOString().slice(0, 16);
      document.getElementById('fechaaperturacaja').value = formattedDate;
  });