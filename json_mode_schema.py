from litellm import completion 
from config import MODEL
import json

schema = {
    "name": "OrderExtraction",
    "schema":{
        "type": "object",
        "properties": { # Define the properties of the order
            "order_id":{"type": "string"},
            "customer":{ # Nested object for customer details -> schema for customer
                "type": "object",
                "properties":{
                    "name":{"type": "string"},
                    "email":{"type": "string"}
                },
                "required": ["name", "email"] # Make sure name and email are always present
            },
            "items":{ #` Array of items in the order -> schema for each item
                "type": "array",
                "items":{
                    "type": "object",
                    "properties":{
                        "sku": {"type": "string"},
                        "name": {"type": "string"},
                        "qty": {"type": "integer"},
                        "price": {"type": "number"}
                    }
                },
                "required": ["sku", "name", "qty", "price"]
            },
            "total": {"type": "number"},
            "currency": {"type": "string"}
        } ,
        "required": ["order_id", "customer", "items", "total", "currency"],
        "additionalProperties": False
    },
    "strict": True
}

messages = [
    {"role":"system","content":"Return ONLY a JSON object matching the schema."},
    {"role":"user","content":"Order A-1029 by Sarah Johnson : 2x Water Bottle ($12.50 each), 1x Carrying Pouch ($5). Total $30."}
]

resp = completion(
    model=MODEL,
    messages=messages, # ข้อความที่ส่งไปให้โมเดล
    response_format={"type": "json_schema", "json_schema": schema} # ตัวกำหนดให้ output ต้องเป็น JSON ที่ตรงตาม schema ที่เรากำหนดไว้ในตัวแปร schema
)
content = resp.choices[0].message["content"] # ดึงข้อความที่โมเดลตอบกลับมา
print("\nParsed:\n", json.dumps(json.loads(content), indent=2)) # แสดงผลลัพธ์ที่ได้ในรูปแบบ JSON ที่อ่านง่าย
