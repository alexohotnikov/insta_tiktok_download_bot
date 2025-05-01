"""
Module for storing GIF-related constants and utilities.
"""

PROCESSING_GIFS = [
    {
        "id": "1",
        "url": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExemVqOGNvNTJ4NDJ3OXN2b2g4aWhubHY3ZzJrcnYwZW5yanV2NGNuYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5oYgxQKHhEjEk/giphy.gif",
        "thumb": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExemVqOGNvNTJ4NDJ3OXN2b2g4aWhubHY3ZzJrcnYwZW5yanV2NGNuYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5oYgxQKHhEjEk/giphy.gif" 
    }, 
    {
        "id": "2",
        "url": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbHRhcHliZ3I5ZWtycnE3Z2k3bXlvazY4NTNmNnRjdDhiaGkxcThpdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5Zesu5VPNGJlm/giphy.gif",
        "thumb": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbHRhcHliZ3I5ZWtycnE3Z2k3bXlvazY4NTNmNnRjdDhiaGkxcThpdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5Zesu5VPNGJlm/giphy.gif"
    },
    {
        "id": "3",
        "url": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmo1ZDZrbGFmdm54OWZtM25rY3A2NXRoZjNjODk4b2QxZHdxZHVnNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/9A51YP5RfEaM2PjiNP/giphy.gif",
        "thumb": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmo1ZDZrbGFmdm54OWZtM25rY3A2NXRoZjNjODk4b2QxZHdxZHVnNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/9A51YP5RfEaM2PjiNP/giphy.gif"
    },
    {
        "id": "4",
        "url": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXF3c25jdGEwaG9qMnhlbzRqdTN1ZWZrMmltYzFqejNrZ211NW02MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Lh2ujv7Unkm4noHHzu/giphy.gif",
        "thumb": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXF3c25jdGEwaG9qMnhlbzRqdTN1ZWZrMmltYzFqejNrZ211NW02MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Lh2ujv7Unkm4noHHzu/giphy.gif"
    },
    {
        "id": "5",
        "url": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHp0eTQwdDBranZqeDJkYWI5Yjg0YWM5emw0bXFjenUyNXprd29kdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fs6yE0mCGBXBfB5mvZ/giphy.gif",
        "thumb": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHp0eTQwdDBranZqeDJkYWI5Yjg0YWM5emw0bXFjenUyNXprd29kdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fs6yE0mCGBXBfB5mvZ/giphy.gif"
    },
    {
        "id": "6",
        "url": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTc3NjllM3VzYWxvamQwb2E4Ymdwb3Y3N250YWs0dWh0Y2E5cHUwMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LPn77YyDIqfhm/giphy.gif",
        "thumb": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTc3NjllM3VzYWxvamQwb2E4Ymdwb3Y3N250YWs0dWh0Y2E5cHUwMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LPn77YyDIqfhm/giphy.gif"
    },
    {
        "id": "7",
        "url": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2o3czlsYnN0dHZidHJxeXIydGZmN2Yxb3BnOXBnNGlrdzN4Y2w0ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/10FwycrnAkpshW/giphy.gif",
        "thumb": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2o3czlsYnN0dHZidHJxeXIydGZmN2Yxb3BnOXBnNGlrdzN4Y2w0ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/10FwycrnAkpshW/giphy.gif"
    },
    {
        "id": "8",
        "url": "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3NlbzJpZG82OXVvbDZiZjBmcjNzcjhzdXU3cHkyc3dnbjIyc252eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/IRFQYGCokErS0/giphy.gif",
        "thumb": "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3NlbzJpZG82OXVvbDZiZjBmcjNzcjhzdXU3cHkyc3dnbjIyc252eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/IRFQYGCokErS0/giphy.gif"
    },
    {
        "id": "9",
        "url": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExMm1vZXF2ZmY1N3prbDB4dmN1YW12ZjkxZzlmMGNqMmI5ZXN1bG00bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MBh8D7EsXa0KhGFdgj/giphy.gif",
        "thumb": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExMm1vZXF2ZmY1N3prbDB4dmN1YW12ZjkxZzlmMGNqMmI5ZXN1bG00bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MBh8D7EsXa0KhGFdgj/giphy.gif"
    },
    {
        "id": "10",
        "url": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3UxZWdpMWg5YnFscHhmNWduZGpndXB1cWxua3NmZzdqMGRndGxkZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/UTFpFheTbCvfDX6L0o/giphy.gif",
        "thumb": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3UxZWdpMWg5YnFscHhmNWduZGpndXB1cWxua3NmZzdqMGRndGxkZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/UTFpFheTbCvfDX6L0o/giphy.gif"
    }
] 