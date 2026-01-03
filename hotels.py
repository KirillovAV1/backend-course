from fastapi import APIRouter, Query, Body, Path

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Сочи", "name": "Sochi"},
    {"id": 2, "title": "Дубай", "name": "Dubai"},
]


@router.get("",
            summary="Получение списка отелей")
def get_hotels(
        hotel_id: int | None = Query(None, description="ID отеля"),
        title: str | None = Query(None, description="Название отеля (Кириллица)"),
        name: str | None = Query(None, description="Название отеля (Латиница)"),
):
    hotels_ = []
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if title and hotel["title"] != title:
            continue
        if name and hotel["name"] != name:
            continue
        hotels_.append(hotel)
    return hotels_


@router.post("",
             summary="Создание отеля")
def create_hotel(
        title: str = Body(embed=True, description="Название отеля (Кириллица)"),
        name: str = Body(embed=True, description="Название отеля (Латиница)"),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
    return {"status": "OK"}


@router.put("/{hotel_id}",
            summary="Обновление всех полей отеля по hotel_id")
def full_update_hotel(
        hotel_id: int = Path(description="ID отеля"),
        title: str = Body(embed=True, description="Название отеля (Кириллица)"),
        name: str = Body(embed=True, description="Название отеля (Латиница)"),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            break
    return {"status": "OK"}


@router.patch("/{hotel_id}",
              summary="Обновление выбранных полей по hotel_id")
def partial_update_hotel(
        hotel_id: int = Path(description="ID отеля"),
        title: str = Body(embed=True, description="Название отеля (Кириллица)"),
        name: str = Body(embed=True, description="Название отеля (Латиница)"),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
            break
    return {"status": "OK"}


@router.delete("/{hotel_id}",
               summary="Удаление отеля по hotel_id")
def delete_hotel(
        hotel_id: int = Path(description="ID отеля")
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
