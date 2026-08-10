# 📖 SPIDY AI — MEMORY USAGE & REST API GUIDE

## 1. Natural Memory Commands

### Save Preferences & Facts
- *"Hey Spidy, remember that I use VS Code"*
- *"Hey Spidy, my favorite language is Python"*

### Memory Context Resolution
- *"Hey Spidy, open my editor"* ➔ (Launches VS Code)
- *"Hey Spidy, what is my favorite language?"* ➔ (Responds "Python")

### Query & List Memories
- *"Hey Spidy, what do you remember about me?"*

### Delete Memories
- *"Hey Spidy, forget my preferred editor"*
- *"Hey Spidy, forget everything"* ➔ (Requires explicit confirmation)

---

## 2. REST API Memory Endpoints

### List Memories
- **GET** `/api/memory`
- **GET** `/api/memory?category=PREFERENCE`

### Save Memory
- **POST** `/api/memory`
- **Request Body:**
```json
{
  "key": "preferred_editor",
  "value": "VS Code",
  "category": "PREFERENCE"
}
```

### Delete Single Memory
- **DELETE** `/api/memory/preferred_editor`

### Clear All Memories
- **POST** `/api/memory/clear`
