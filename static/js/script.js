document.addEventListener('DOMContentLoaded', function() {
    const getPosts = document.getElementById('getPosts');
    const profileUrls = document.getElementById('profileUrls');
    const postsTable = document.getElementById('postsTable');
    const loading = document.getElementById('loading');

    console.log('Script loaded');

    getPosts.addEventListener('click', function() {
        const urls = profileUrls.value.split('\n').filter(url => url.trim() !== '');
        
        if (urls.length === 0) {
            alert('Please enter at least one LinkedIn profile URL.');
            return;
        }

        loading.classList.remove('hidden');
        postsTable.classList.add('hidden');

        fetch('/get_posts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ profileUrls: urls }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data);
            const tbody = postsTable.querySelector('tbody');
            tbody.innerHTML = '';

            data.forEach(post => {
                const row = tbody.insertRow();
                row.insertCell(0).textContent = post.profile;
                row.insertCell(1).textContent = post.content;
                row.insertCell(2).textContent = post.time;
                
                const urlCell = row.insertCell(3);
                const link = document.createElement('a');
                link.href = post.url;
                link.textContent = 'View Post';
                link.target = '_blank';
                urlCell.appendChild(link);

                const draftReplyCell = row.insertCell(4);
                const draftReplyLink = document.createElement('a');
                draftReplyLink.href = post.draft_reply;
                draftReplyLink.textContent = 'Draft Reply';
                draftReplyLink.target = '_blank';
                draftReplyCell.appendChild(draftReplyLink);
            });

            loading.classList.add('hidden');
            postsTable.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            loading.classList.add('hidden');
            alert('An error occurred while fetching posts. Please check the console for details.');
        });
    });
});