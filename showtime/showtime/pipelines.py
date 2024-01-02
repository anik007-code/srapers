import re

from itemadapter import ItemAdapter


class ShowtimePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # field_names = adapter.field_names()
        # for field_name in field_names:
        #     if field_name != 'title':
        #         value = adapter.get(field_name)
        #         adapter[field_name] = value.strip()
        title = adapter.get('title')
        if title is not None:
            adapter['title'] = title.strip()

        views = adapter.get('views')
        if views is not None:
            views = views.replace(':', '').strip()
            adapter['views'] = views

        return item

