import { useWindowVirtualizer } from '@tanstack/react-virtual';
import { useEffect, useRef, useState } from 'react';

interface VirtualGridProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  estimateSize?: number;
  keyExtractor: (item: T) => string | number;
}

export function VirtualGrid<T>({ 
  items, 
  renderItem, 
  estimateSize = 450, 
  keyExtractor 
}: VirtualGridProps<T>) {
  const parentRef = useRef<HTMLDivElement>(null);
  const [isMounted, setIsMounted] = useState(false);
  const [columns, setColumns] = useState(3);

  useEffect(() => {
    setIsMounted(true);
    const updateColumns = () => {
      const width = window.innerWidth;
      if (width >= 1280) setColumns(3);      // xl
      else if (width >= 768) setColumns(2);  // md - lg
      else setColumns(1);                   // xs - sm
    };
    updateColumns();
    window.addEventListener('resize', updateColumns);
    return () => window.removeEventListener('resize', updateColumns);
  }, []);

  const rowCount = Math.ceil(items.length / columns);

  const virtualizer = useWindowVirtualizer({
    count: rowCount,
    estimateSize: () => estimateSize,
    overscan: 5,
    scrollMargin: parentRef.current?.offsetTop ?? 0,
  });

  const virtualRows = virtualizer.getVirtualItems();

  if (!isMounted) return null;

  return (
    <section ref={parentRef} className="relative w-full">
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          width: '100%',
          position: 'relative',
        }}
      >
        {virtualRows.map((virtualRow) => {
          const startIndex = virtualRow.index * columns;
          const rowItems = items.slice(startIndex, startIndex + columns);

          return (
            <div
              key={virtualRow.key}
              data-index={virtualRow.index}
              ref={virtualizer.measureElement}
              className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 pb-6"
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                transform: `translateY(${virtualRow.start - virtualizer.options.scrollMargin}px)`,
              }}
            >
              {rowItems.map((item) => (
                <div key={keyExtractor(item)} className="h-full">
                  {renderItem(item)}
                </div>
              ))}
            </div>
          );
        })}
      </div>
    </section>
  );
}
