document.addEventListener("DOMContentLoaded", function () {
    fetch('data/contenu.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur de chargement des données');
            }
            return response.json();
        })
        .then(data => {
            console.log("Fichier JSON chargé avec succès");
            const mainContent = document.getElementById('main-content');

            data.forEach(anime => {
                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                    <img src="${anime.image}" alt="${anime.title}">
                    <h3>${anime.title}</h3>
                `;

                // Ajouter l'événement de clic sur la carte
                card.addEventListener('click', () => {
                    openModal(anime);
                });

                mainContent.appendChild(card);
            });
        })
        .catch(error => {
            console.error('Erreur de chargement des données:', error);
        });
});

// Ouvrir la fenêtre modale
function openModal(anime) {
    const modal = document.getElementById('modal');
    const animeTitle = document.getElementById('anime-title');
    const animeDescription = document.getElementById('anime-description');
    const seasonSelect = document.getElementById('season-select');
    const episodeList = document.getElementById('episode-list');

    animeTitle.textContent = anime.title;
    animeDescription.textContent = anime.description;

    // Vider les sélections précédentes
    seasonSelect.innerHTML = '';
    episodeList.innerHTML = '';

    // Remplir le select avec les saisons
    anime.seasons.forEach(season => {
        const option = document.createElement('option');
        option.value = season.season;
        option.textContent = season.season;
        seasonSelect.appendChild(option);
    });

    // Afficher les épisodes de la première saison par défaut
    if (anime.seasons.length > 0) {
        seasonSelect.value = anime.seasons[0].season;
        updateEpisodes(anime.seasons[0].episodes);
    }

    // Écouter le changement de saison
    seasonSelect.addEventListener('change', () => {
    const selectedSeason = anime.seasons.find(season => season.season === seasonSelect.value);
    episodeList.innerHTML = ''; // Vider la liste des épisodes
    selectedSeason.episodes.forEach(episode => {
        const episodeLink = document.createElement('a');
        episodeLink.href = `player.html?link=${encodeURIComponent(episode.link)}`; // Redirige vers le lecteur vidéo
        episodeLink.className = 'episode-link';
        episodeLink.textContent = episode.title;
        episodeList.appendChild(episodeLink);
    });
});

    modal.style.display = 'block'; // Afficher la fenêtre modale
}

// Mettre à jour la liste des épisodes
function updateEpisodes(episodes) {
    const episodeList = document.getElementById('episode-list');
    episodeList.innerHTML = ''; // Vider la liste précédente

    episodes.forEach(episode => {
        const episodeLink = document.createElement('a');
        episodeLink.href = `player.html?link=${encodeURIComponent(episode.link)}`; // Redirige vers le lecteur vidéo
        episodeLink.className = 'episode-link';
        episodeLink.textContent = episode.title;
        episodeList.appendChild(episodeLink);
    });
}

// Fermer la fenêtre modale
document.getElementById('close-modal').onclick = function () {
    document.getElementById('modal').style.display = 'none';
}

// Fermer la fenêtre modale si l'utilisateur clique en dehors de la fenêtre
window.onclick = function (event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}
