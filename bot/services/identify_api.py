import aiohttp
import asyncio
import aiofiles
from aiohttp import ClientTimeout


async def upload_image(session: aiohttp.ClientSession, image_path: str) -> str:
    """Загружает изображение и возвращает его ID."""
    form_data = aiohttp.FormData()
    async with aiofiles.open(image_path, 'rb') as f:
        form_data.add_field('file', await f.read(), filename='image', content_type='image/jpeg')


    async with session.post('https://api.plantnet.org/v1/images', data=form_data) as resp:
        json_id = await resp.json()
        return json_id['id']

async def identify_plant(session: aiohttp.ClientSession, image_url: str) -> dict:
    """Идентифицирует растение по URL изображения."""
    data = {"images": [{"url": image_url}]}
    params = {
        "illustratedOnly": "true",
        "clientType": "web",
        "clientVersion": "3.0.0",
        "lang": "ru",
        "kt": "true",
        "mediaSource": "file"
    }
    async with session.post(
        "https://api.plantnet.org/v1/projects/k-world-flora/queries/identify",
        params=params,
        json=data
    ) as resp:
        return await resp.json()

async def get_plant_info(session: aiohttp.ClientSession, species_name: str, author: str) -> dict:
    """Получает информацию о растении по его названию и автору."""
    url = f"https://api.plantnet.org/v1/projects/k-world-flora/species/{species_name} {author}"
    params = {"lang": "ru", "truncated": "true"}
    async with session.get(url, params=params) as resp:
        data = await resp.json()
        return {
            'species': data['species']['name'],
            'genus': data['genus']['name'],
            'family': data['family']['name'],
            'author': data['species']['author'],
            'common_names': data.get('commonNames', []),
            'images': {
                image_type: data['images'].get(image_type, [{}])[0].get('o')
                for image_type in ['leaf', 'flower', 'habit', 'bark', 'other']
            },
            'cabi_link': next((link for link in data.get('links', []) if 'cabi' in link), None)
        }

async def identify_plant_from_image(image_path: str) -> dict:
    """Идентифицирует растение по изображению и возвращает информацию о нем."""
    async with aiohttp.ClientSession(timeout=ClientTimeout(total=10)) as session:
        image_id = await upload_image(session, image_path)
        image_url = f"https://bs.plantnet.org/v1/image/o/{image_id}"
        json_answer = await identify_plant(session, image_url)
        first_result = json_answer['results'][0]
        species_name = first_result['species']['name']
        author = first_result['species']['author']
        return await get_plant_info(session, species_name, author)