import pandas as pd
import matplotlib.pyplot as plt

class WildberriesUnitEconomics:
    def __init__(self):
        self.data = None
        self.report = None

    def input_data(self):
        """Модуль ввода данных: загрузка данных от пользователя или из файла."""
        print("Введите данные для расчета юнит-экономики:")
        
        data = {
            'Название товара': input("Название товара: "),
            'Цена закупки': float(input("Цена закупки (руб): ")),
            'Цена продажи': float(input("Цена продажи (руб): ")),
            'Категория': input("Категория товара: "),
            'Вес (кг)': float(input("Вес товара (кг): ")),
            'Комиссия WB (%)': float(input("Комиссия Wildberries (%): ")),
            'Логистика до WB (руб)': float(input("Логистика до склада WB (руб): ")),
            'Хранение (руб/ед/мес)': float(input("Стоимость хранения (руб/ед/мес): ")),
            'Процент выкупа (%)': float(input("Процент выкупа (%): ")),
            'Доп. расходы (упаковка и пр.)': float(input("Доп. расходы (руб): ")),
        }

        if data['Цена продажи'] <= data['Цена закупки']:
            raise ValueError("Ошибка: цена продажи должна быть выше закупочной цены.")
        
        self.data = pd.DataFrame([data])
        print("\nДанные успешно загружены.")
        return self.data

    def calculate_metrics(self):
        """Модуль расчета: вычисление ключевых показателей юнит-экономики."""
        if self.data is None:
            raise ValueError("Данные не загружены. Сначала введите данные.")
        
        df = self.data.copy()
        
        df['Комиссия WB (руб)'] = df['Цена продажи'] * (df['Комиссия WB (%)'] / 100)
        
        df['Себестоимость'] = (
            df['Цена закупки'] + 
            df['Логистика до WB (руб)'] + 
            df['Хранение (руб/ед/мес)'] + 
            df['Доп. расходы (упаковка и пр.)'] + 
            df['Комиссия WB (руб)']
        )
        
        df['Выручка'] = df['Цена продажи'] * (df['Процент выкупа (%)'] / 100)
        df['Прибыль'] = df['Выручка'] - df['Себестоимость']
        df['Маржинальность (%)'] = (df['Прибыль'] / df['Выручка']) * 100
        
        self.report = df
        print("\nРасчет показателей завершен.")
        return self.report

    def visualize_data(self):
        """Модуль визуализации с улучшенным круговым графиком."""
        if self.report is None:
            raise ValueError("Сначала выполните расчет показателей.")
        
        df = self.report.copy()
        product_name = df['Название товара'].iloc[0]
        
        plt.figure(figsize=(16, 10))
        
        # круговой график структуры затрат
        plt.subplot(2, 2, 1)
        cost_components = {
            'Закупка': df['Цена закупки'].iloc[0],
            'Логистика': df['Логистика до WB (руб)'].iloc[0],
            'Хранение': df['Хранение (руб/ед/мес)'].iloc[0],
            'Упаковка': df['Доп. расходы (упаковка и пр.)'].iloc[0],
            'Комиссия WB': df['Комиссия WB (руб)'].iloc[0]
        }
        
        explode = [0.1 if v/sum(cost_components.values()) > 0.2 else 0 
                  for v in cost_components.values()]
        
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
        
        wedges, texts, autotexts = plt.pie(
            cost_components.values(),
            labels=cost_components.keys(),
            autopct=lambda p: f'{p:.1f}%\n({p*sum(cost_components.values())/100:.0f} руб)',
            startangle=90,
            explode=explode,
            colors=colors,
            textprops={'fontsize': 9},
            pctdistance=0.85
        )
        
        centre_circle = plt.Circle((0,0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.title('Детальная структура затрат', pad=20)
        
        plt.legend(
            wedges,
            [f'{k}: {v:.1f} руб' for k,v in cost_components.items()],
            title="Компоненты затрат",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1))
        
        # Остальные графики (без изменений)
        plt.subplot(2, 2, 2)
        metrics = {
            'Выручка': df['Выручка'].iloc[0],
            'Себестоимость': df['Себестоимость'].iloc[0],
            'Прибыль': df['Прибыль'].iloc[0]
        }
        plt.bar(metrics.keys(), metrics.values(), color=['green', 'pink', 'orange'])
        plt.title('Основные финансовые показатели')
        plt.ylabel('Рубли')
        
        plt.subplot(2, 2, 3)
        plt.bar(['Маржинальность'], df['Маржинальность (%)'], color='purple')
        plt.title(f'Маржинальность: {df["Маржинальность (%)"].iloc[0]:.1f}%')
        plt.ylabel('%')
        
        plt.subplot(2, 2, 4)
        comparison = {
            'Цена продажи': df['Цена продажи'].iloc[0],
            'Себестоимость': df['Себестоимость'].iloc[0]
        }
        plt.bar(comparison.keys(), comparison.values(), color=['green', 'red'])
        plt.title('Сравнение цены продажи и себестоимости')
        plt.ylabel('Рубли')
        
        plt.suptitle(f'Анализ юнит-экономики товара: {product_name}', fontsize=16)
        plt.tight_layout()
        plt.show()

    def export_to_csv(self, filename='wildberries_unit_economics_report.csv'):
        """Модуль экспорта: сохранение отчета в CSV файл."""
        if self.report is None:
            raise ValueError("Сначала выполните расчет показателей.")
        
        self.report.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\nОтчет успешно сохранен в файл: {filename}")

# Пример использования
if __name__ == "__main__":
    wb = WildberriesUnitEconomics()
    wb.input_data()
    report = wb.calculate_metrics()
    print("\nОтчет:")
    print(report)
    wb.visualize_data()
    wb.export_to_csv()
    