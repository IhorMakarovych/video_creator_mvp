def save_video_to_disk(video_data: bytes, filename: str) -> str:
    filepath = f"./videos/{filename}"
    with open(filepath, "wb") as f:
        f.write(video_data)
    return filepath