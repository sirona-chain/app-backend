from flask import Blueprint, g, request, Response, jsonify, stream_with_context
from app.web.hooks import login_required, load_model
from app.web.db.models import User, Conversation
from app.chat import build_chat, ChatArgs
from flask_cors import CORS

bp = Blueprint("conversation", __name__, url_prefix="/api/conversations")
CORS(bp, supports_credentials=True)


@bp.route("/", methods=["GET"])
# @login_required
@load_model(User, lambda r: r.args.get("user_id"))
def list_conversations(user):
    return [c.as_dict() for c in user.conversations]

@bp.route("/", methods=["POST"])
# @login_required
@load_model(User, lambda r: r.args.get("user_id"))
def create_conversation():
    conversation = Conversation.create(user_id=g.user.id)

    return conversation.as_dict()


@bp.route("/<string:conversation_id>/messages", methods=["POST"])
# @login_required
@load_model(Conversation)
def create_message(conversation):
    input = request.json.get("input")
    streaming = request.args.get("stream", False)

    chat_args = ChatArgs(
        conversation_id=conversation.id,
        streaming=streaming,
        metadata={
            "conversation_id": conversation.id,
            "user_id": g.user.id,
        },
    )

    chat = build_chat(chat_args)

    if not chat:
        return "Chat not yet implemented!"

    if streaming:
        return Response(
            stream_with_context(chat.stream(input)), mimetype="text/event-stream"
        )
    else:
        return jsonify({"role": "assistant", "content": chat.run(input)})
