"""Another module with APIRouter"""
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Let's say you also have the endpoints dedicated to handling "Items" 
# from your application in the module `at app/routers/items.py`.

# You have path operations for:
    # /items/
    # /items/{item_id}

# It's all the same structure as with app/routers/users.py.
    # But let's say that this time we are more lazy.
    # And we don't want to have to explicitly type /items/ and tags=["items"] in
    # every path operation (we will be able to do it later)
    
@router.get("/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]


@router.get("/{item_id}")
async def read_item(item_id: str):
    return {"name": "Fake Specific Item", "item_id": item_id}

## Add some custom tags, responses, and dependencies
@router.put(
        "/{item_id}",
        # We are not adding 
        # the prefix `/items/` 
        # nor the `tags=["items"]` 
        # as we will add them later.

        # But we can add custom tags and responses 
        # that will be applied to a specific path operation:
        tags=["custom"],
        responses={403: {"description": "Operation forbidden"}},
        )
async def update_item(item_id: str):
    if item_id != "foo":
        raise HTTPException(status_code=403, detail="You can only update the item: foo")
    return {"item_id": item_id, "name": "The Fighters"}

