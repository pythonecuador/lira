def to_widget(container):
    return container.content.text.__self__


def is_visible(widget):
    def is_gt_zero(obj):
        if isinstance(obj, int):
            return obj > 0
        return obj.min > 0 and obj.max > 0

    height = widget.window.height
    width = widget.window.height
    return is_gt_zero(height) or is_gt_zero(width)
