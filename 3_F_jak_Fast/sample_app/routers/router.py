from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]