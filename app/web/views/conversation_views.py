from flask import Blueprint, g, request, Response, jsonify, stream_with_context
from flask_cors import CORS
from app.web.hooks import login_required, load_model
from app.web.db.models import User, Conversation
from app.chat import build_chat, ChatArgs

bp = Blueprint("conversation", __name__, url_prefix="/api/conversations")
CORS(bp, supports_credentials=True)

@bp.route("/", methods=["GET"])
@login_required
@load_model(User, lambda r: r.args.get("user_id"))
def list_conversations(user):
    return [c.as_dict() for c in user.conversations]

@bp.route("/", methods=["POST"])
@login_required
@load_model(User, lambda r: r.args.get("user_id"))
def create_conversation(user):
    conversation = Conversation.create(user_id=user.id)

    return conversation.as_dict()


@bp.route("/<string:conversation_id>/messages", methods=["POST"])
@login_required
@load_model(User, lambda r: r.args.get("user_id"))
def create_message(user, conversation_id):
    print("conversation_id", conversation_id)
    conversation = user.conversations[0]
    input_text = request.json.get("input")
    streaming = request.args.get("stream", False)

    print("Received input:", input_text)

    chat_args = ChatArgs(
        conversation_id=conversation.id,
        streaming=streaming,
        metadata={"conversation_id": conversation.id, "user_id": g.user.id},
    )
    print("before try")

    try:
        chat = build_chat(chat_args)
        print("Built chat:", chat)
        
        if not chat:
            return jsonify({"error": "Chat not yet implemented!"}), 501
        
        input_dict = {"input": input_text}

        if streaming:
            return Response(stream_with_context(chat.stream(input_dict)), mimetype="text/event-stream")
        else:
            result = chat.run(input_dict)
            print("Chat run result:", result)
            return jsonify({"role": "assistant", "text": result})
    except Exception as e:
        print("Error running chat:", e)
        return jsonify({"error": str(e)}), 500
