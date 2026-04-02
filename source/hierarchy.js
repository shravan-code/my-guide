/**
 * hierarchy.js - Sidebar Navigation Hierarchy Data
 * Use this file to maintain the sidebar menu structure.
 * Paths are relative to source/ directory.
 */

var sidebarHierarchy = [
  {
    section: 'bigdata',
    label: 'Big Data',
    href: 'data/index.html',
    icon: '<path d="M12 3C7.58 3 4 4.79 4 7s3.58 4 8 4 8-1.79 8-4-3.58-4-8-4zM4 9v3c0 2.21 3.58 4 8 4s8-1.79 8-4V9c-2.42 1.66-5.88 2.66-8 2.66S6.42 10.66 4 9zm0 5v3c0 2.21 3.58 4 8 4s8-1.79 8-4v-3c-2.42 1.66-5.88 2.66-8 2.66S6.42 15.66 4 14z"/>',
    children: [
      { label: 'Overview', href: 'data/index.html' },
      {
        section: 'data',
        label: 'Data',
        href: 'data/index.html',
        children: [
          { label: 'Formats', href: 'data/data-formats.html' },
          { label: 'Pipelines', href: 'data/data-pipeline.html' },
          { label: 'Quality', href: 'data/data-quality.html' },
          { label: 'Types', href: 'data/data-types.html' }
        ]
      }
    ]
  },
  {
    section: 'cloud',
    label: 'Cloud',
    href: 'cloud/index.html',
    icon: '<path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z"/>',
    children: [
      { label: 'Overview', href: 'cloud/index.html' },
      { label: 'Architecture', href: 'cloud/cloud-topics.html' },
      {
        section: 'providers',
        label: 'Providers',
        href: 'cloud/index.html',
        children: [
          {
            section: 'aws',
            label: 'AWS',
            href: 'cloud/cloud-aws.html',
            children: [
              { label: 'Domains', href: 'cloud/cloud-aws.html' },
              { label: 'Services', href: 'cloud/cloud-aws.html' }
            ]
          },
          { label: 'Azure', href: 'cloud/cloud-azure.html' },
          { label: 'GCP', href: 'cloud/cloud-gcp.html' }
        ]
      },
      {
        section: 'fundamentals',
        label: 'Fundamentals',
        href: 'cloud/cloud-basics.html',
        children: [
          { label: 'Basics', href: 'cloud/cloud-basics.html' },
          { label: 'Compute', href: 'cloud/cloud-compute.html' },
          { label: 'Serverless', href: 'cloud/cloud-serverless.html' },
          { label: 'Services', href: 'cloud/cloud-services.html' },
          { label: 'Storage', href: 'cloud/cloud-storage.html' }
        ]
      },
      {
        section: 'apis',
        label: 'APIs',
        href: 'apis/index.html',
        children: [
          { label: 'Overview', href: 'apis/index.html' },
          { label: 'Concepts', href: 'apis/concepts.html' },
          { label: 'Types', href: 'apis/types.html' }
        ]
      }
    ]
  },
  {
    section: 'languages',
    label: 'Languages',
    href: 'languages/index.html',
    icon: '<path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/>',
    children: [
      {
        section: 'python',
        label: 'Python',
        href: 'python/index.html',
        children: [
          { label: 'Overview', href: 'python/index.html' },
          { label: 'Fundamentals', href: 'python/python-fundamentals.html' },
          { label: 'OOPs', href: 'python/python-oops.html' },
          { label: 'Methods', href: 'python/python-methods.html' },
          { label: 'Memory', href: 'python/memory-performance.html' }
        ]
      },
      {
        section: 'libraries',
        label: 'Libraries',
        href: 'libraries/libraries-hub.html',
        children: [
          { label: 'Overview', href: 'libraries/libraries-hub.html' },
          {
            section: 'pandas',
            label: 'Pandas',
            href: 'pandas/index.html',
            children: [
              { label: 'Overview', href: 'pandas/index.html' },
              { label: 'Series', href: 'pandas/pandas-series.html' },
              { label: 'DataFrames', href: 'pandas/pandas-dataframes.html' },
              { label: 'Methods', href: 'pandas/methods.html' }
            ]
          },
          {
            section: 'numpy',
            label: 'NumPy',
            href: 'numpy/index.html',
            children: [
              { label: 'Overview', href: 'numpy/index.html' },
              { label: 'Basics', href: 'numpy/numpy-basics.html' },
              { label: 'Arrays', href: 'numpy/numpy-arrays.html' },
              { label: 'Operations', href: 'numpy/numpy-operations.html' },
              { label: 'Methods', href: 'numpy/methods.html' }
            ]
          },
          {
            section: 'spark',
            label: 'Spark',
            href: 'spark/index.html',
            children: [
              { label: 'Overview', href: 'spark/index.html' },
              { label: 'Theory', href: 'spark/spark-theory.html' },
              { label: 'Architecture', href: 'spark/spark-architecture.html' },
              { label: 'Code', href: 'spark/spark-code.html' }
            ]
          }
        ]
      },
      {
        section: 'frameworks',
        label: 'Frameworks',
        href: 'tools/index.html',
        children: [
          { label: 'Overview', href: 'tools/index.html' },
          { label: 'dbt', href: 'tools/dbt.html' },
          { label: 'Airflow', href: 'tools/airflow.html' },
          { label: 'Kafka', href: 'tools/kafka.html' }
        ]
      }
    ]
  },
  {
    section: 'database',
    label: 'Database',
    href: 'sql/index.html',
    icon: '<path d="M12 3C7.58 3 4 4.79 4 7s3.58 4 8 4 8-1.79 8-4-3.58-4-8-4zM4 9v3c0 2.21 3.58 4 8 4s8-1.79 8-4V9c-2.42 1.66-5.88 2.66-8 2.66S6.42 10.66 4 9zm0 5v3c0 2.21 3.58 4 8 4s8-1.79 8-4v-3c-2.42 1.66-5.88 2.66-8 2.66S6.42 15.66 4 14z"/>',
    children: [
      { label: 'Overview', href: 'sql/index.html' },
      { label: 'Modelling', href: 'sql/sql-modelling.html' },
      { label: 'Concepts', href: 'sql/sql-concepts.html' },
      {
        section: 'postgresql',
        label: 'PostgreSQL',
        href: 'sql/sql-queries.html',
        children: [
          { label: 'Queries', href: 'sql/sql-queries.html' },
          { label: 'Methods', href: 'sql/sql-methods.html' },
          { label: 'Joins', href: 'sql/sql-joins.html' },
          { label: 'Subqueries', href: 'sql/sql-subqueries.html' },
          { label: 'Windows', href: 'sql/sql-windows.html' }
        ]
      },
      { label: 'Practice', href: 'sql/sql-queries.html' }
    ]
  },
  {
    section: 'cheatsheets',
    label: 'Cheatsheet',
    href: 'cheatsheets/cheatsheet.html',
    icon: '<path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-1.9-2-2zm-2 14H8v-2h8v2zm0-4H8v-2h8v2zm-3-4H8V6h5v2z"/>',
    children: [
      { label: 'Overview', href: 'cheatsheets/cheatsheet.html' },
      { label: 'Python', href: 'cheatsheets/python-cheatsheet.html' },
      { label: 'Pandas', href: 'cheatsheets/pandas-cheatsheet.html' },
      { label: 'NumPy', href: 'cheatsheets/numpy-cheatsheet.html' },
      { label: 'Spark', href: 'cheatsheets/spark-cheatsheet.html' },
      { label: 'PostgreSQL', href: 'cheatsheets/postgresql-cheatsheet.html' },
      { label: 'Compare', href: 'cheatsheets/compare.html' }
    ]
  },
  {
    section: 'differences',
    label: 'Differences',
    href: 'differences/differences-hub.html',
    icon: '<path d="M12 3L4 9v6l8 6 8-6v-6l-8-6z"/>',
    children: [
      { label: 'Overview', href: 'differences/differences-overview.html' },
      { label: 'Python', href: 'differences/differences-python.html' },
      { label: 'Pandas', href: 'differences/differences-pandas.html' },
      { label: 'Numpy', href: 'differences/differences-numpy.html' },
      { label: 'Spark', href: 'differences/differences-spark.html' },
      { label: 'SQL', href: 'differences/differences-sql.html' },
      { label: 'Airflow', href: 'differences/differences-airflow.html' },
      { label: 'DBT', href: 'differences/differences-dbt.html' },
      { label: 'Kafka', href: 'differences/differences-kafka.html' },
      { label: 'AWS', href: 'differences/differences-aws.html' },
      { label: 'Cloud', href: 'differences/differences-cloud.html' },
      { label: 'Databricks', href: 'differences/differences-databricks.html' },
      { label: 'Data Modelling', href: 'differences/differences-data-modelling.html' }
    ]
  },
  {
    section: 'roadmaps',
    label: 'Roadmap',
    href: 'roadmaps/roadmap.html',
    icon: '<path d="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM15 19l-6-2.11V5l6 2.11V19z"/>',
    children: [
      { label: 'Overview', href: 'roadmaps/roadmap.html' },
      { label: 'SQL', href: 'roadmaps/sql-roadmap.html' },
      { label: 'Python', href: 'roadmaps/python-roadmap.html' },
      { label: 'Spark', href: 'roadmaps/spark-roadmap.html' },
      { label: 'Data Engineer', href: 'roadmaps/data-engineer-roadmap.html' },
      { label: 'ML Engineer', href: 'roadmaps/ml-engineer-roadmap.html' },
      { label: 'AI Engineer', href: 'roadmaps/ai-engineer-roadmap.html' }
    ]
  },
  {
    section: 'portfolio',
    label: 'Portfolio',
    href: 'portfolios/portfolio.html',
    icon: '<path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>',
    children: [
      { label: 'Overview', href: 'portfolios/portfolio.html' },
      {
        section: 'projects',
        label: 'Projects',
        href: 'portfolios/portfolio.html',
        children: [
          { label: 'Self', href: 'portfolios/projects/projects-self.html' },
          { label: 'Experienced', href: 'portfolios/projects/projects-experienced.html' }
        ]
      }
    ]
  }
];
