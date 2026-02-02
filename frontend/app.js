const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const searchError = document.getElementById('searchError');
const searchResults = document.getElementById('searchResults');

// Save form elements
const isbnInput = document.getElementById('isbnInput');
const titleInput = document.getElementById('titleInput');
const authorInput = document.getElementById('authorInput');
const yearInput = document.getElementById('yearInput');
const saveBookBtn = document.getElementById('saveBookBtn');
const listbooksBtn = document.getElementById('listbooksBtn');
const booksList = document.getElementById('booksList'); 




// Initialize
document.addEventListener('DOMContentLoaded', () => {
    
    if (searchBtn) {
        searchBtn.addEventListener('click', handleSearch);
    }

    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                handleSearch();
            }
        });
    }

    if (saveBookBtn) {
        saveBookBtn.addEventListener('click', () => {
            addBook();
        });
    }

    // "All books" button
    if (listbooksBtn) {
        listbooksBtn.addEventListener('click', () => {
            loadBooks();
        });
    }
});

function populateSaveForm(book) {
    isbnInput.value = book.isbn || '';
    titleInput.value = book.title || '';
    authorInput.value = book.author || '';
    yearInput.value = book.publication_year || '';
}


// Search Books
async function handleSearch() {
    const query = searchInput.value.trim();
    
    if (!query) {
        showError('Please enter a search query');
        return;
    }
    
    hideError();
    searchResults.innerHTML = '<p class="loading">Searching...</p>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/books/search?query=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error(`Search failed: ${response.statusText}`);
        }
        
        const results = await response.json();
        displaySearchResults(results);
    } catch (error) {
        console.error('Search error:', error);
        showError(`Failed to search books: ${error.message}`);
        searchResults.innerHTML = '';
    }
}

function displaySearchResults(results) {
    if (results.length === 0) {
        searchResults.innerHTML = '<p class="empty-state">No books found. Try a different search.</p>';
        return;
    }
    
    searchResults.innerHTML = results.map(book => `
        <div class="search-result-item">
            <h3>${escapeHtml(book.title)}</h3>
            <p><strong>Author:</strong> ${escapeHtml(book.author || 'Unknown')}</p>
            ${book.publication_year ? `<p><strong>Year:</strong> ${book.publication_year}</p>` : ''}
            ${book.isbn ? `<p><strong>ISBN:</strong> ${escapeHtml(book.isbn)}</p>` : ''}
            <button class="add-btn" onclick="populateSaveForm(${JSON.stringify(book)})">
                Use this book
            </button>
        </div>
    `).join('');
}

// Add Book
async function addBook(bookData) {
    try {
        const response = await fetch(`${API_BASE_URL}/books/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                isbn: bookData.isbn,
                title: bookData.title,
                author: bookData.author,
                publication_year: bookData.publication_year
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to add book');
        }
        
        // Clear search and reload books
        searchInput.value = '';
        searchResults.innerHTML = ''
        
        // Show success message (optional)
        alert('Book added successfully!');
    } catch (error) {
        console.error('Add book error:', error);
        alert(`Failed to add book: ${error.message}`);
    }
}

// Load Books
async function loadBooks() {
    if (!booksList) return;
    booksList.innerHTML = '<p class="loading">Loading books...</p>';
    try {
        const response = await fetch(`${API_BASE_URL}/books`);
        
        if (!response.ok) {
            throw new Error(`Failed to load books: ${response.statusText}`);
        }
        
        const books = await response.json();
        displayBooks(books);
    } catch (error) {
        console.error('Load books error:', error);
        booksList.innerHTML = `<p class="error-message show">Failed to load books: ${error.message}</p>`;
    }
}

function displayBooks(books) {
    if (!booksList) return;
    if (books.length === 0) {
        booksList.innerHTML = '<p class="empty-state">No books yet. Search and add some books!</p>';
        return;
    }
    
    booksList.innerHTML = books.map(book => `
        <div class="book-card">
            <div class="book-info">
                <h3>${escapeHtml(book.title)}</h3>
                <p><strong>Author:</strong> ${escapeHtml(book.author || 'Unknown')}</p>
                ${book.publication_year ? `<p><strong>Year:</strong> ${book.publication_year}</p>` : ''}
                ${book.isbn ? `<p><strong>ISBN:</strong> ${escapeHtml(book.isbn)}</p>` : ''}
                <span class="book-status status-${book.status.toLowerCase()}">
                    ${book.status}
                </span>
            </div>
            <div class="book-actions">
                <button 
                    class="action-btn mark-read-btn" 
                    onclick="markAsRead(${book.id})"
                    ${book.status === 'Read' ? 'disabled' : ''}
                >
                    Mark as Read
                </button>
                <button 
                    class="action-btn delete-btn" 
                    onclick="deleteBook(${book.id})"
                >
                    Delete
                </button>
            </div>
        </div>
    `).join('');
}

// Mark as Read
async function markAsRead(bookId) {
    try {
        const response = await fetch(`${API_BASE_URL}/books/${bookId}`, {
            method: 'PUT'
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to update book');
        }
        
        loadBooks();
    } catch (error) {
        console.error('Mark as read error:', error);
        alert(`Failed to mark as read: ${error.message}`);
    }
}

// Delete Book
async function deleteBook(bookId) {
    if (!confirm('Are you sure you want to delete this book?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/books/${bookId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to delete book');
        }
        
        loadBooks();
    } catch (error) {
        console.error('Delete book error:', error);
        alert(`Failed to delete book: ${error.message}`);
    }
}

// Utility Functions
function showError(message) {
    searchError.textContent = message;
    searchError.classList.add('show');
}

function hideError() {
    searchError.classList.remove('show');
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showSaveError(message) {
    if (!saveError) return;
    saveError.textContent = message;
    saveError.classList.add('show');
}

function hideSaveError() {
    if (!saveError) return;
    saveError.classList.remove('show');
}
